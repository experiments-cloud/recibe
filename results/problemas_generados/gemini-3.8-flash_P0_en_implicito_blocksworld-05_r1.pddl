(define (problem BLOCKS-7-0)
  (:domain BLOCKS)
  (:objects
    a b c d e f g - block
  )
  (:init
    (handempty)
    (ontable d)
    (on c d)
    (on f c)
    (on a f)
    (on b a)
    (on g b)
    (on e g)
    (clear e)
  )
  (:goal
    (and
      (on a g)
      (on g d)
      (on d b)
      (on b c)
      (on c f)
      (on f e)
    )
  )
)
