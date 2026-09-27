(define (problem blocksworld-problema)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (ontable a)
    (ontable b)
    (ontable c)
    (ontable d)
    (handempty)
  )
  (:goal (and
    (on d c)
    (on c b)
    (on b a)
  ))
)
