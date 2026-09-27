(define (problem blocksworld-problema)
  (:domain BLOCKS)
  (:objects
    a b c d e f - block
  )
  (:init
    (ontable c)
    (handempty)
    (on e c)
    (on f e)
    (on b f)
    (on d b)
    (on a d)
    (clear a)
  )
  (:goal (and
    (on e f)
    (on f a)
    (on a b)
    (on b c)
    (on c d)
  ))
)
