(define (problem blocksworld-problema)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (clear f)
    (handempty)
    (on f e)
    (on e b)
    (ontable b)
    (clear d)
    (on d a)
    (on a c)
    (ontable c)
  )
  (:goal (and
    (on c b)
    (on b a)
    (on a e)
    (on e f)
    (on f d)
  ))
)
